from generators import mp_organizations


def load_mp_organizations(conn, tables, count: int):
    if count <= 3:
        raise Exception("Слишком маленькое количество организаций")

    children_count = count // 3
    parents_count = count - children_count

    parent_orgs = mp_organizations.generate_parent_mp_organizations(parents_count)
