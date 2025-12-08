from typing import List, Dict, Set

class GeonameQueryExpansionHelper:

    # Define which DB columns depend on which JOIN
    FIELD_TO_JOIN_MAP = {
        "country_name": "country",
        "postal_code_regex": "country",

        "admin1_name": "admin1",
    }

    # Define JOIN groups → what fields they supply
    JOIN_TO_FIELDS_MAP = {
        "country": {"country_name", "postal_code_regex"},
        "admin1": {"admin1_name"},
    }

    @staticmethod
    def get_required_joins(expand_fields: List[str]) -> Set[str]:
        """Return only the joins required for the fields in expand."""
        joins = {
            GeonameQueryExpansionHelper.FIELD_TO_JOIN_MAP[f]
            for f in expand_fields
            if f in GeonameQueryExpansionHelper.FIELD_TO_JOIN_MAP
        }
        return joins

    @staticmethod
    def get_required_fields(expand_fields: List[str]) -> Set[str]:
        """Return only the fields that are valid for expansion."""
        return {
            f for f in expand_fields
            if f in GeonameQueryExpansionHelper.FIELD_TO_JOIN_MAP
        }
