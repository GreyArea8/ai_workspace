@app.route("/task", methods=["POST"])
def add_task():
    data = request.get_json() or {}
    task_item = data.get("task")
    if task_item:
        task_queue.append(task_item)
        return jsonify({"status": "queued", "task": task_item, "queue_length": len(task_queue)}), 200
    return jsonify({"error": "No task provided"}), 400
