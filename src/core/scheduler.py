# src/core/scheduler.py
import threading
import time

class Scheduler:
    """Task scheduler for periodic data generation."""
    
    def __init__(self):
        """Initialize the scheduler."""
        self.tasks = {}
        self.running = False
    
    def schedule(self, interval, function, *args, **kwargs):
        """
        Schedule a function to run periodically.
        
        Args:
            interval: Time interval in seconds
            function: Function to run
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Task identifier
        """
        task_id = len(self.tasks) + 1
        
        # Create task
        task = {
            'interval': interval,
            'function': function,
            'args': args,
            'kwargs': kwargs,
            'next_run': time.time(),
            'running': True
        }
        
        self.tasks[task_id] = task
        
        # Start task thread if not already running
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._run_tasks)
            thread.daemon = True
            thread.start()
            
        return task_id
        
    def _run_tasks(self):
        """Run scheduled tasks."""
        while self.running and self.tasks:
            current_time = time.time()
            
            # Check each task
            for task_id, task in list(self.tasks.items()):
                if not task['running']:
                    continue
                    
                if current_time >= task['next_run']:
                    # Run the task
                    try:
                        task['function'](*task['args'], **task['kwargs'])
                    except Exception as e:
                        print(f"Error running task {task_id}: {e}")
                        
                    # Schedule next run
                    task['next_run'] = current_time + task['interval']
            
            # Sleep to avoid high CPU usage
            time.sleep(0.1)
    
    def cancel(self, task_id):
        """
        Cancel a scheduled task.
        
        Args:
            task_id: Task identifier to cancel
        """
        if task_id in self.tasks:
            self.tasks[task_id]['running'] = False
    
    def stop(self):
        """Stop all scheduled tasks."""
        self.running = False
        
        # Wait for tasks to complete
        time.sleep(0.2)