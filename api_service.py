def background_autonomous_worker():
    """Continuously evaluates queued tasks and executes background operations."""
    global agent_status
    while True:
        agent_status = "RUNNING"
        if task_queue:
            task = task_queue.pop(0)
            print(f"Executing autonomous task: {task}")
            
            # Autonomous execution routing based on task type
            if "survey" in task.lower() or "offer" in task.lower():
                print("Targeting micro-task / offer completion pipeline...")
                # Add automated request logic targeting payout endpoints
            elif "diagnostic" in task.lower():
                print("Processing automated vehicle diagnostic dataset...")
        else:
            agent_status = "IDLE"
        time.sleep(5)
