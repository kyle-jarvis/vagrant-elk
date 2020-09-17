"""
Utilities and helpers for the vagrant-elk-examples project.
"""


def compose_es_query():
    """
    Compose a dictionary to be submitted as a match query to an ES server.
    """
    allowed_fields = {0: "firstname", 1: "surname", 2: "city", 3: "employer"}
    good_keys = [str(x) for x in allowed_fields]
    prompt = "\n".join(["{k}. {v}".format(k=k, v=allowed_fields[k]) for k in range(len(allowed_fields))])
    print("Select a field to query:")
    print(prompt)
    good_answer = False
    while not good_answer:
        result = input()
        result.strip()
        if result in good_keys:
            good_answer = True
        else:
            print("Allowed inputs are {}".format(good_keys))
    print("Input a value to search for..")
    value = input()
    query={allowed_fields[int(result)] : value}
    print("Query: {}".format(query))
    return query
