import json, copy

src = "products_backup.json"
dst = "products_backup_mapped.json"

with open(src, "r", encoding="utf-8") as f:
    data = json.load(f)

def map_fields(fields: dict) -> dict:
    f = fields.copy()
    if "name" in f:
        f["product_name"] = f.pop("name")
    if "product_image" in f:
        f["images"] = f.pop("product_image")
    if "created_at" in f:
        f["created_date"] = f.pop("created_at")
    # if your model has this new field, set a default
    f.setdefault("is_approved", False)
    return f

out = []
for obj in data:
    if isinstance(obj, dict) and obj.get("model", "").endswith(".product"):
        obj = copy.deepcopy(obj)
        obj["fields"] = map_fields(obj.get("fields", {}))
    out.append(obj)

with open(dst, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("✅ Wrote", dst)
