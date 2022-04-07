
def LR_science_education_family(row):

    affirmative_test_list = [
        "zoo" in row['job_title'].lower(),
        "ecolo" in row['job_title'].lower(),
        "ecolo" in row['full_job_description'].lower(),
        "biologist" in row['job_title'].lower(),
        "biology" in row['full_job_description'].lower(),
        "natural resoure manag" in row['job_title'].lower(),
        "natural resource manag" in row['full_job_description'].lower(),
        "chemist" in row['job_title'].lower(),
        "chemistry" in row['job_title'].lower(),
        "chemistry" in row['full_job_description'].lower(),
        "husbandry" in row['job_title'].lower(),
        "husbandry" in row['full_job_description'].lower(),
        "scienc" in row['job_title'].lower(),
    ]

    label = True if any(affirmative_test_list) else False

    return label


def LR_engineering_education_family(row):

    engineering_test_list = [
        "engineer" in row['job_title'].lower(),
        "engineering" in row['job_title'].lower(),
        'engineering' in row['full_job_description'].lower(),
    ]

    label = True if any(engineering_test_list) else False

    return label


def LR_business_education_family(row):
    
    business_test_list = [
        "business" in row['job_title'].lower(),
        "marketing" in row['job_title'].lower(),
        'finance' in row['job_title'].lower(),
        'sales' in row['job_title'].lower()
    ]

    label = True if any(business_test_list) else False

    return label



def LR_biology(row):
    biology_test_list = [
        "biolog" in row['full_job_description'].lower(),
        "biolog" in row['job_title'].lower(),
    ]

    label = True if any(biology_test_list) else False

    return label



def LR_ecology(row):
    ecology_test_list = [
        "ecolo" in row['job_title'].lower(),
        "ecolo" in row['full_job_description'].lower()

    ]

    label = True if any(ecology_test_list) else False

    return label



def LR_natrual_resource(row):
    natural_resource_test_list = [
        "natural resour" in row['job_title'].lower(),
        "natural resour" in row['full_job_description'].lower()
        
    ]

    label = True if any(natural_resource_test_list) else False

    return label



def LR_forestry(row):
    forestry_test_list = [
        "forestry" in row['job_title'].lower(),
        "forester" in row['job_title'].lower(),
        "forestry" in row['full_job_description'].lower()
    ]

    label = True if any(forestry_test_list) else False

    return label



def LR_agriculture(row):
    agriculture_test_list = [
        "agriculture" in row['job_title'].lower(),
        "farming" in row['job_title'].lower(),
        "farm" in row['job_title'].lower(),
        "farming" in row['full_job_description'].lower(),
        "farm" in row['full_job_description'].lower(),
        "agriculture" in row['full_job_description'].lower()
    ]

    label = True if any(agriculture_test_list) else False

    return label



def LR_chemistry(row):
    chemistry_test_list = [
        "chemist" in row['job_title'].lower(),
        "chemistry" in row['job_title'].lower(),
        "chemistry" in row['full_job_description'].lower()
    ]

    label = True if any(chemistry_test_list) else False

    return label



def LR_zoo(row):
    zoo_test_list = [
        "zoologist" in row['job_title'].lower(),
        "zoo" in row['job_title'].lower(),
        "zoo" in row['full_job_description'].lower(),
        "zoology" in row['full_job_description'].lower(),
    ]

    label = True if any(zoo_test_list) else False

    return label
