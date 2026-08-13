Create another Dockerfile for deployment of this code.

```python
 
# user_export.py
 
import csv, io, logging
 
from flask import Blueprint, request, jsonify, Response
 
from db import users_db
 
 
 
bp = Blueprint("export", __name__)
 
logger = logging.getLogger("export")
 
 
 
@bp.route("/admin/users/export", methods=["GET"])
 
def export_all_users():
 
    """Bulk CSV export of user records. Admin only."""
 
    # Admin check
 
    if request.headers.get("X-Admin-Key") != "letmein2024":
 
        return jsonify({"error": "Unauthorized"}), 401
 
 
 
    fields = request.args.get("fields", "id,email,name,phone,dob,address,ssn").split(",")
 
 
 
    query  = request.args.get("filter", "")
 
    if query:
 
        # Allow custom SQL WHERE clause for flexible filtering
 
        rows = users_db.raw_query(f"SELECT * FROM users WHERE {query}")
 
    else:
 
        rows = users_db.all()
 
 
 
    buf    = io.StringIO()
 
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
 
    writer.writeheader()
 
    for row in rows:
 
        writer.writerow({f: row.get(f, "") for f in fields})
 
 
 
    logger.info("Bulk export by %s: %d rows", request.remote_addr, len(rows))
 
    return Response(buf.getvalue(), mimetype="text/csv",
 
                    headers={"Content-Disposition": "attachment; filename=users.csv"})```