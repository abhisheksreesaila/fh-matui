# 🚀 Enhanced DataTableResource Implementation Guide

## 📋 Overview

This enhancement adds **CrudTable-style features** to the existing `DataTableResource` class without breaking changes:

✅ **CrudContext** dataclass for rich hook context  
✅ **Enhanced hooks**: `on_create`, `on_update`, `on_delete` with full request state  
✅ **Async/sync support** for external API integration  
✅ **HX-Trigger auto-refresh** for seamless table updates  
✅ **Backward compatible** - existing code works unchanged  

---

## 📁 Files Created

1. **`datatable_enhancement.xml`** - New cells to add (CrudContext + documentation)
2. **`datatable_resource_enhanced.xml`** - Enhanced DataTableResource class
3. **`IMPLEMENTATION_GUIDE.md`** - This file

---

## 🔧 Implementation Steps

### Step 1: Add CrudContext Documentation & Code

**Location:** After the `DataTable` function cell, before the existing `DataTableResource` markdown

Open `datatable_enhancement.xml` and copy cells:
- Cell 1: CrudContext documentation (markdown)
- Cell 2: CrudContext dataclass (#| export)
- Cell 3: show_doc(CrudContext)

**Paste these 3 cells** into your notebook after line ~472 (after `DataTable` function ends).

---

### Step 2: Replace DataTableResource Documentation

**Location:** Find the existing cell that starts with `## 🔧 DataTableResource`

Replace that markdown cell with **Cell 4** from `datatable_enhancement.xml`.

This adds:
- 🆕 Enhanced CRUD Hooks table
- Request State Accessors documentation
- Usage examples (basic, async hooks, soft delete, read-only sync)

---

### Step 3: Replace DataTableResource Class

**Location:** Find the cell with `class DataTableResource:`

Replace the **entire class cell** with the enhanced version from `datatable_resource_enhanced.xml`.

**Key changes:**
- Added `on_create`, `on_update`, `on_delete` hook parameters
- Added `get_user`, `get_db`, `get_table` accessors
- Added `_call_hook()` and `_build_context()` methods
- Enhanced `_handle_table()` with auto-refresh container
- Enhanced `_handle_action()` DELETE to use new hook
- Enhanced `_handle_save()` CREATE/UPDATE to use new hooks
- Enhanced `_success_toast()` to return HTMLResponse with HX-Trigger

---

## ✅ Testing Checklist

After implementation, test:

1. **Existing functionality** - Run existing demos, ensure no breakage
2. **New CrudContext** - Verify `show_doc(CrudContext)` displays properly
3. **Enhanced hooks** - Test examples from documentation
4. **Auto-refresh** - Verify table refreshes after create/update/delete
5. **Async support** - Test async hook examples
6. **Backward compatibility** - Verify legacy hooks still work

---

## 📖 Usage Examples

### Basic (No Changes)
```python
# Existing code works exactly the same
resource = DataTableResource(
    app=app,
    base_route="/products",
    columns=product_columns,
    get_all=get_products,
    get_by_id=get_product_by_id,
    create=create_product,
    update=update_product,
    delete=delete_product,
    title="Products"
)
```

### 🆕 With Async External API
```python
async def quiltt_create_connection(ctx: CrudContext) -> dict:
    api = QuilttAPI()
    response = await api.create_connection(
        institution=ctx.record['institution_name'],
        user_id=ctx.user['user_id']
    )
    ctx.record['connection_id'] = response['id']
    ctx.record['status'] = 'pending'
    return ctx.record

DataTableResource(
    app=app,
    base_route="/connections",
    columns=connection_columns,
    get_all=get_connections,
    get_by_id=get_connection_by_id,
    create=insert_connection,
    update=update_connection,
    delete=delete_connection,
    title="Bank Connections",
    on_create=quiltt_create_connection,  # 🆕
    get_user=lambda req: req.state.user
)
```

### 🆕 With Soft Delete
```python
def soft_delete_budget(ctx: CrudContext) -> None:
    ctx.tbl.update({
        'id': ctx.record_id,
        'is_deleted': True,
        'deleted_at': datetime.now().isoformat(),
        'deleted_by': ctx.user['user_id']
    })

DataTableResource(
    app=app,
    base_route="/budgets",
    columns=budget_columns,
    get_all=get_active_budgets,
    get_by_id=get_budget_by_id,
    create=create_budget,
    update=update_budget,
    delete=None,
    title="Budgets",
    on_delete=soft_delete_budget,  # 🆕
    get_user=lambda req: req.state.user,
    get_table=lambda req: req.state.tables['budgets']
)
```

---

## 🎯 Key Benefits

1. **External API Integration** - Perfect for services like Quiltt, Stripe, Plaid
2. **Rich Context** - Full access to request, user, db, table in hooks
3. **Async Support** - Hooks can await external API calls
4. **Auto-Refresh** - Table updates automatically via HX-Trigger
5. **Zero Breaking Changes** - Existing code continues working
6. **Soft Deletes** - Easy implementation with custom delete hooks
7. **Multi-Tenant** - Request state accessors support complex apps

---

## 📝 Next Steps

1. **Copy cells** from XML files into notebook
2. **Test examples** - Run notebook and verify functionality
3. **Update LLM context** - Run `python generate_llms_ctx.py`
4. **Commit changes** - `.\git_commit_push.ps1 "Add enhanced DataTableResource with CrudContext"`
5. **Update docs** - Run `nbdev_prepare` to rebuild documentation

---

## 🐛 Troubleshooting

**Issue:** `NameError: name 'CrudContext' is not defined`  
**Fix:** Ensure CrudContext cell has `#| export` directive and comes before DataTableResource

**Issue:** Auto-refresh not working  
**Fix:** Check that `_success_toast()` returns `HTMLResponse` with `HX-Trigger` header

**Issue:** Async hook not awaiting  
**Fix:** Verify `_call_hook()` uses `asyncio.iscoroutinefunction()` check

**Issue:** CrudContext fields are None  
**Fix:** Provide `get_user`, `get_db`, `get_table` accessors in DataTableResource init

---

## 📚 Documentation

After implementation, the following will be auto-generated:
- API docs for `CrudContext`
- API docs for enhanced `DataTableResource`
- Usage examples in module documentation
- LLM context file updates

---

**Built with ❤️ for fh-matui - Making FastHTML CRUD development effortless!**
