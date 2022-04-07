import pandas as pd

import enums


class BaseFeatureEngineering:
    def __init__(self, dataframe, simple_fields):
        self.dataframe = dataframe
        self.simple_fields = simple_fields

    def location_parser(self):
        for geo_feature in (("City", "CityName"), ("State", "CountrySubDivisionCode")):
            self.dataframe[
                f"{geo_feature[0]}_Mix"
            ] = self.dataframe.PositionLocation.apply(
                lambda record: [
                    location[geo_feature[1]] if geo_feature[1] in location else None
                    for location in record
                ]
            )
            self.dataframe[f"{geo_feature[0]}_Unique_Count"] = self.dataframe[
                f"{geo_feature[0]}_Mix"
            ].apply(lambda record: len(set(record)))
            self.dataframe[f"{geo_feature[0]}_Total_Count"] = self.dataframe[
                f"{geo_feature[0]}_Mix"
            ].apply(lambda record: len(record))

    def simple_field_parser(self):
        for field in self.simple_fields:
            self.dataframe[field] = self.dataframe[field].apply(
                lambda field: [record["Name"] for record in field]
            )
            self.dataframe[field] = self.dataframe[field].apply(lambda x: x[0])

    def build(self):
        for func in [self.location_parser, self.simple_field_parser]:
            func()

        return self.dataframe


class ExtendedFeatureEngineering:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    @staticmethod
    def parse_details(df):
        for add_on in enums.EXTENSION_ADDONS:
            df[add_on] = df["Details"].apply(
                lambda x: [x[add_on] if add_on in x else None]
            )
        return df

    @staticmethod
    def unpack_brackets(df):
        for field in enums.EXTENSION_UNPACK_BRACKETED:
            df[field] = df[field].apply(lambda x: x[0])
        return df

    @staticmethod
    def unpack_lists(df):
        for field in enums.EXTENSION_LIST_FIELDS:
            df[field] = df[field].apply(lambda x: x[0])
        return df

    def userarea_parser(self):
        for field in ["Details", "IsRadialSearch"]:
            self.dataframe[field] = self.dataframe["UserArea"].apply(lambda x: x[field])
        self.dataframe = self.dataframe.drop(["UserArea"], axis=1)

    def build(self):
        for func in [self.userarea_parser]:
            func()

        self.dataframe = self.parse_details(self.dataframe).drop(["Details"], axis=1)
        self.dataframe = self.unpack_brackets(self.dataframe)
        self.dataframe = self.unpack_lists(self.dataframe)
        return self.dataframe
