"""Transaction Rules Service - Manages rule creation, execution, and application"""

import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from storage.db_models import TransactionRule, Transaction
from utils.sql_util import get_sql_util
from services.category.category_service import get_category_service


class RuleCondition:
    """Represents a single rule condition"""

    def __init__(self, field: str, operator: str, value: str):
        self.field = field  # e.g., "merchant_name", "description", "amount"
        self.operator = operator  # e.g., "contains", "equals", "greater_than"
        self.value = value

    def to_dict(self):
        return {"field": self.field, "operator": self.operator, "value": self.value}

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            field=data.get("field"),
            operator=data.get("operator"),
            value=data.get("value"),
        )


class RuleAction:
    """Represents a single rule action"""

    def __init__(self, action_type: str, parameters: Dict[str, Any]):
        self.action_type = action_type  # e.g., "set_category", "set_memo", "set_tags"
        self.parameters = (
            parameters  # e.g., {"master_category": "Food", "sub_category": "Dining"}
        )

    def to_dict(self):
        return {"action_type": self.action_type, "parameters": self.parameters}

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            action_type=data.get("action_type"), parameters=data.get("parameters", {})
        )


class TransactionRulesService:
    """Service for managing transaction categorization rules"""

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.logger = logging.getLogger(__name__)

    def create_rule(
        self,
        rule_name: str,
        conditions: List[Dict],
        actions: List[Dict],
        created_by: str,
        exceptions: List[Dict] = None,
        priority: int = 0,
        stop_processing: bool = False,
        apply_to_existing: bool = False,
    ) -> TransactionRule:
        """Create a new transaction rule using SqlUtil"""
        try:
            sql_util = get_sql_util(self.tenant_id)

            # Create rule data as dictionary (don't include id, let database auto-generate)
            rule_data = {
                "rule_name": rule_name,
                "rule_conditions": json.dumps(conditions),
                "rule_actions": json.dumps(actions),
                "rule_exceptions": json.dumps(exceptions) if exceptions else None,
                "priority": priority,
                "stop_processing": stop_processing,
                "is_active": True,
                "apply_to_existing": apply_to_existing,
                "created_by": created_by,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "last_run_at": None,
                "transactions_affected": 0,
                # Don't include 'id' - let database auto-generate it
            }

            # Insert using SqlUtil (will auto-generate ID)
            result = sql_util.insert(TransactionRule, rule_data)

            # If apply_to_existing is True, run the rule immediately
            if apply_to_existing and result:
                rule_id = getattr(result, "id", None)
                if rule_id:
                    self.apply_rule(rule_id)

            self.logger.info(f"Created rule '{rule_name}' for tenant {self.tenant_id}")
            return result

        except Exception as e:
            self.logger.error(f"Error creating rule: {e}")
            import traceback

            traceback.print_exc()
            raise

    def get_all_rules(self) -> List[TransactionRule]:
        """Get all rules for the tenant using SqlUtil"""
        try:
            sql_util = get_sql_util(self.tenant_id)
            results = sql_util.execute_query("rule_find_all")

            if not results:
                return []

            # Convert to TransactionRule objects
            rules = []
            for row in results:
                rule_dict = dict(row)
                # Parse JSON fields
                if rule_dict.get("rule_conditions"):
                    rule_dict["rule_conditions"] = json.loads(
                        rule_dict["rule_conditions"]
                    )
                if rule_dict.get("rule_actions"):
                    rule_dict["rule_actions"] = json.loads(rule_dict["rule_actions"])
                if rule_dict.get("rule_exceptions"):
                    rule_dict["rule_exceptions"] = json.loads(
                        rule_dict["rule_exceptions"]
                    )

                rules.append(TransactionRule(**rule_dict))

            return rules

        except Exception as e:
            self.logger.error(f"Error fetching rules: {e}")
            return []

    def get_active_rules(self) -> List[TransactionRule]:
        """Get all active rules sorted by priority using SqlUtil"""
        try:
            sql_util = get_sql_util(self.tenant_id)
            results = sql_util.execute_query("rule_find_active")

            if not results:
                return []

            # Convert to TransactionRule objects
            rules = []
            for row in results:
                rule_dict = dict(row)
                # Parse JSON fields
                if rule_dict.get("rule_conditions"):
                    rule_dict["rule_conditions"] = json.loads(
                        rule_dict["rule_conditions"]
                    )
                if rule_dict.get("rule_actions"):
                    rule_dict["rule_actions"] = json.loads(rule_dict["rule_actions"])
                if rule_dict.get("rule_exceptions"):
                    rule_dict["rule_exceptions"] = json.loads(
                        rule_dict["rule_exceptions"]
                    )

                rules.append(TransactionRule(**rule_dict))

            return rules

        except Exception as e:
            self.logger.error(f"Error fetching active rules: {e}")
            return []

    def update_rule(self, rule_id: int, updates: Dict) -> bool:
        """Update an existing rule using SqlUtil"""
        try:
            sql_util = get_sql_util(self.tenant_id)

            # Get existing rule first
            results = sql_util.execute_query("rule_find_by_id", {"rule_id": rule_id})
            if not results:
                self.logger.error(f"Rule {rule_id} not found")
                return False

            existing_rule = dict(results[0])

            # Merge updates
            updates["updated_at"] = datetime.utcnow().isoformat()
            updated_data = {**existing_rule, **updates}

            # Serialize JSON fields if they're dicts/lists
            for field in ["rule_conditions", "rule_actions", "rule_exceptions"]:
                if field in updated_data and isinstance(
                    updated_data[field], (dict, list)
                ):
                    updated_data[field] = json.dumps(updated_data[field])

            # Use execute_update with rule_update query
            affected = sql_util.execute_update(
                "rule_update", {**updated_data, "rule_id": rule_id}
            )

            self.logger.info(f"Updated rule {rule_id} for tenant {self.tenant_id}")
            return affected > 0

        except Exception as e:
            self.logger.error(f"Error updating rule {rule_id}: {e}")
            return False

    def delete_rule(self, rule_id: int) -> bool:
        """Delete a rule using SqlUtil"""
        try:
            sql_util = get_sql_util(self.tenant_id)
            affected = sql_util.execute_update(
                "rule_delete_by_id", {"rule_id": rule_id}
            )

            self.logger.info(f"Deleted rule {rule_id} for tenant {self.tenant_id}")
            return affected > 0

        except Exception as e:
            self.logger.error(f"Error deleting rule {rule_id}: {e}")
            return False

    def toggle_rule_status(self, rule_id: int, is_active: bool) -> bool:
        """Enable or disable a rule"""
        return self.update_rule(rule_id, {"is_active": is_active})

    def apply_rule(self, rule_id: int) -> Dict[str, Any]:
        """Apply a specific rule to all matching transactions using SqlUtil"""
        try:
            sql_util = get_sql_util(self.tenant_id)

            # Get the rule using SqlUtil
            results = sql_util.execute_query("rule_find_by_id", {"rule_id": rule_id})
            if not results:
                return {"success": False, "message": "Rule not found"}

            rule_dict = dict(results[0])

            # Parse conditions and actions
            conditions = json.loads(rule_dict["rule_conditions"])
            actions = json.loads(rule_dict["rule_actions"])

            # Find matching transactions using efficient SQL query
            matching_transactions = self._find_matching_transactions(conditions)

            # Apply actions to matching transactions
            affected_count = 0
            for txn in matching_transactions:
                if self._apply_actions_to_transaction(txn, actions):
                    affected_count += 1

            # Update rule stats using SqlUtil
            sql_util.execute_update(
                "rule_update_stats",
                {
                    "rule_id": rule_id,
                    "last_run_at": datetime.utcnow().isoformat(),
                    "transactions_affected": affected_count,
                    "updated_at": datetime.utcnow().isoformat(),
                },
            )

            self.logger.info(f"Applied rule {rule_id} to {affected_count} transactions")

            return {
                "success": True,
                "affected_count": affected_count,
                "message": f"Successfully applied rule to {affected_count} transactions",
            }

        except Exception as e:
            self.logger.error(f"Error applying rule {rule_id}: {e}")
            import traceback

            traceback.print_exc()
            return {"success": False, "message": str(e)}

    def apply_rules_to_new_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Apply all active rules to a newly added transaction using SqlUtil"""
        try:
            sql_util = get_sql_util(self.tenant_id)

            # Get the transaction using SqlUtil
            results = sql_util.execute_query(
                "transaction_find_by_id", {"transaction_id": transaction_id}
            )
            if not results:
                return {"success": False, "message": "Transaction not found"}

            txn_dict = dict(results[0])
            txn = Transaction(**txn_dict)

            # Get active rules
            active_rules = self.get_active_rules()

            rules_applied = []
            for rule in active_rules:
                conditions = (
                    rule.rule_conditions
                    if isinstance(rule.rule_conditions, list)
                    else json.loads(rule.rule_conditions)
                )
                actions = (
                    rule.rule_actions
                    if isinstance(rule.rule_actions, list)
                    else json.loads(rule.rule_actions)
                )

                # Check if transaction matches conditions
                if self._transaction_matches_conditions(txn, conditions):
                    # Apply actions
                    if self._apply_actions_to_transaction(txn, actions):
                        rules_applied.append(rule.rule_name)

                        # Stop processing if rule says so
                        if rule.stop_processing:
                            break

            return {
                "success": True,
                "rules_applied": rules_applied,
                "message": f"Applied {len(rules_applied)} rules to transaction",
            }

        except Exception as e:
            self.logger.error(
                f"Error applying rules to transaction {transaction_id}: {e}"
            )
            return {"success": False, "message": str(e)}

    def preview_rule_matches(self, rule_id: int, limit: int = 100) -> List[Dict]:
        """
        Preview transactions that would match a rule's conditions using SqlUtil.
        Returns a list of transaction dictionaries with key fields for display.
        """
        try:
            sql_util = get_sql_util(self.tenant_id)

            # Get the rule using SqlUtil
            results = sql_util.execute_query("rule_find_by_id", {"rule_id": rule_id})
            if not results:
                self.logger.error(f"Rule {rule_id} not found")
                return []

            rule_dict = dict(results[0])

            # Parse conditions
            conditions = json.loads(rule_dict["rule_conditions"])

            # Get matching transactions
            matching_transactions = self._find_matching_transactions(conditions)

            # Limit results and format for display
            limited_transactions = matching_transactions[:limit]

            # Format transactions for grid display
            formatted = []
            for txn in limited_transactions:
                if isinstance(txn, dict):
                    txn_dict = txn
                else:
                    txn_dict = txn.__dict__ if hasattr(txn, "__dict__") else {}

                formatted.append(
                    {
                        "Transaction Id": txn_dict.get("transaction_id", ""),
                        "Date": (
                            txn_dict.get("transaction_date", "")[:10]
                            if txn_dict.get("transaction_date")
                            else ""
                        ),
                        "Merchant": txn_dict.get("transaction_merchant_name", "")
                        or txn_dict.get("transaction_description", "N/A"),
                        "Amount": txn_dict.get("transaction_amount", "0"),
                        "Category": txn_dict.get(
                            "fingoal_enrichment_response_categorydescription",
                            "Uncategorized",
                        ),
                        "Master Category": txn_dict.get(
                            "fingoal_enrichment_response_highlevelcategorydescription",
                            "",
                        ),
                        "Description": txn_dict.get("transaction_description", ""),
                    }
                )

            self.logger.info(
                f"Preview for rule {rule_id}: {len(formatted)} matching transactions"
            )
            return formatted

        except Exception as e:
            self.logger.error(f"Error previewing rule matches: {e}")
            import traceback

            traceback.print_exc()
            return []

    def _find_matching_transactions(self, conditions: List[Dict]) -> List:
        """Find all transactions matching the given conditions using efficient SQL query"""
        try:
            sql_util = get_sql_util(self.tenant_id)

            # Build SQL WHERE clause dynamically from conditions
            where_parts = []
            params = {}

            field_mapping = {
                "merchant_name": "transaction_merchant_name",
                "description": "transaction_description",
                "amount": "transaction_amount",
                "simple_description": "fingoal_enrichment_response_simpledescription",
                "original_description": "fingoal_enrichment_response_originaldescription",
                "merchant_type": "fingoal_enrichment_response_merchanttype",
                "category_label": "fingoal_enrichment_response_categorylabel",
            }

            for idx, condition in enumerate(conditions):
                field = condition.get("field")
                operator = condition.get("operator")
                value = condition.get("value", "")

                actual_field = field_mapping.get(field, field)
                param_name = f"cond_{idx}"

                if operator == "contains":
                    where_parts.append(f'LOWER("{actual_field}") LIKE :{param_name}')
                    params[param_name] = f"%{value.lower()}%"
                elif operator == "equals":
                    where_parts.append(f'LOWER("{actual_field}") = :{param_name}')
                    params[param_name] = value.lower()
                elif operator == "starts_with":
                    where_parts.append(f'LOWER("{actual_field}") LIKE :{param_name}')
                    params[param_name] = f"{value.lower()}%"
                elif operator == "ends_with":
                    where_parts.append(f'LOWER("{actual_field}") LIKE :{param_name}')
                    params[param_name] = f"%{value.lower()}"
                elif operator == "greater_than":
                    where_parts.append(
                        f'CAST("{actual_field}" AS NUMERIC) > :{param_name}'
                    )
                    params[param_name] = float(value)
                elif operator == "less_than":
                    where_parts.append(
                        f'CAST("{actual_field}" AS NUMERIC) < :{param_name}'
                    )
                    params[param_name] = float(value)
                elif operator == "not_contains":
                    where_parts.append(
                        f'LOWER("{actual_field}") NOT LIKE :{param_name}'
                    )
                    params[param_name] = f"%{value.lower()}%"

            if not where_parts:
                # No conditions, return all transactions
                results = sql_util.execute_query("transaction_find_all")
            else:
                # Build query with WHERE clause
                where_clause = " AND ".join(where_parts)
                query = f"SELECT * FROM transaction WHERE {where_clause} ORDER BY transaction_date DESC"
                results = sql_util.execute_query(query, params)

            if not results:
                return []

            # Convert to Transaction objects
            matching = []
            for row in results:
                txn_dict = dict(row)
                matching.append(Transaction(**txn_dict))

            return matching

        except Exception as e:
            self.logger.error(f"Error finding matching transactions: {e}")
            import traceback

            traceback.print_exc()
            return []

    def _transaction_matches_conditions(
        self, transaction, conditions: List[Dict]
    ) -> bool:
        """Check if a transaction matches all conditions (AND logic)"""
        try:
            for condition in conditions:
                field = condition.get("field")
                operator = condition.get("operator")
                value = condition.get("value", "").lower()

                # Get transaction field value
                txn_value = self._get_transaction_field_value(transaction, field)
                if txn_value is None:
                    return False

                txn_value = str(txn_value).lower()

                # Apply operator
                if operator == "contains":
                    if value not in txn_value:
                        return False
                elif operator == "equals":
                    if txn_value != value:
                        return False
                elif operator == "starts_with":
                    if not txn_value.startswith(value):
                        return False
                elif operator == "ends_with":
                    if not txn_value.endswith(value):
                        return False
                elif operator == "greater_than":
                    try:
                        if float(txn_value) <= float(value):
                            return False
                    except:
                        return False
                elif operator == "less_than":
                    try:
                        if float(txn_value) >= float(value):
                            return False
                    except:
                        return False
                elif operator == "not_contains":
                    if value in txn_value:
                        return False

            return True  # All conditions matched

        except Exception as e:
            self.logger.error(f"Error checking conditions: {e}")
            return False

    def _get_transaction_field_value(self, transaction, field: str) -> Optional[str]:
        """Get the value of a transaction field"""
        field_mapping = {
            "merchant_name": "transaction_merchant_name",
            "description": "transaction_description",
            "amount": "transaction_amount",
            "simple_description": "fingoal_enrichment_response_simpledescription",
            "original_description": "fingoal_enrichment_response_originaldescription",
            "merchant_type": "fingoal_enrichment_response_merchanttype",
            "category_label": "fingoal_enrichment_response_categorylabel",
        }

        actual_field = field_mapping.get(field, field)
        return getattr(transaction, actual_field, None)

    def _apply_actions_to_transaction(self, transaction, actions: List[Dict]) -> bool:
        """Apply rule actions to a transaction using SqlUtil"""
        try:
            if not self.tenant_id:
                self.logger.error(
                    "tenant_id is required for _apply_actions_to_transaction"
                )
                return False

            from utils.sql_util import get_sql_util

            sql_util = get_sql_util(self.tenant_id)

            updates = {}

            for action in actions:
                action_type = action.get("action_type")
                parameters = action.get("parameters", {})

                if action_type == "set_category":
                    # Set user category from the category hierarchy
                    master_cat = parameters.get("master_category", "")
                    sub_cat = parameters.get("sub_category", "")
                    detail_cat = parameters.get("detail_sub_category", "")

                    # Build category path
                    category_parts = [p for p in [master_cat, sub_cat, detail_cat] if p]
                    updates["usercategory"] = " > ".join(category_parts)

                elif action_type == "set_memo":
                    updates["usermemo"] = parameters.get("memo", "")

                elif action_type == "set_tags":
                    updates["usertags"] = parameters.get("tags", "")

                elif action_type == "delete":
                    # Mark for deletion (you might want to add a deleted flag)
                    updates["usermemo"] = "[DELETED BY RULE]"

            # Apply updates using SqlUtil
            if updates:
                # Get current transaction data and merge with updates
                transaction_id = getattr(transaction, "transaction_id", None)
                if not transaction_id:
                    self.logger.error("Transaction missing transaction_id")
                    return False

                # Ensure all fields required by the query are present
                # If not in updates, try to get from transaction, else default to None
                if "usercategory" not in updates:
                    updates["usercategory"] = getattr(transaction, "usercategory", None)
                if "usermemo" not in updates:
                    updates["usermemo"] = getattr(transaction, "usermemo", None)
                if "usertags" not in updates:
                    updates["usertags"] = getattr(transaction, "usertags", None)

                # Use execute_update with transaction_update_user_fields query
                affected_rows = sql_util.execute_update(
                    "transaction_update_user_fields",
                    {"transaction_id": transaction_id, **updates},
                )

                return affected_rows > 0

            return False

        except Exception as e:
            self.logger.error(f"Error applying actions to transaction: {e}")
            return False

    def get_category_hierarchy(self) -> Dict[str, Any]:
        """Get the complete category hierarchy for the rules builder."""
        try:
            category_service = get_category_service()
            hierarchy = category_service.get_rules_category_hierarchy()

            if hierarchy:
                return hierarchy

            self.logger.warning(
                "No category hierarchy available from CSV, returning empty mapping."
            )
            return {}

        except Exception as e:
            self.logger.error(f"Error fetching category hierarchy from CSV: {e}")
            import traceback

            traceback.print_exc()
            return {}


# Singleton factory pattern
_rules_service = None


def get_transaction_rules_service(tenant_id: str = None) -> TransactionRulesService:
    """Get or create the transaction rules service instance"""
    global _rules_service
    if _rules_service is None or _rules_service.tenant_id != tenant_id:
        _rules_service = TransactionRulesService(tenant_id)
    return _rules_service
