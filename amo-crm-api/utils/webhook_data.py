import re


def fix_webhook_data(data: dict) -> dict:
    contact_lead_index = 0
    new_dict = {}
    for key, value in data.items():
        m = re.match(r"contacts\[\w*\]\[0\]\[linked_leads_id\]\[\d*\]\[ID\]", key)
        if m:
            key = re.sub(
                r"\[linked_leads_id\]\[\d*\]\[ID\]",
                f"[linked_leads_id][{contact_lead_index}][id]",
                key,
            )
            contact_lead_index += 1

        new_dict[key] = value

    return new_dict
