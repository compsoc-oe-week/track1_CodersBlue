class Planner:
    def __init__(self, plan=None):
        self.plan = plan if plan else []
        self.current_step = 0

    def set_plan(self, plan):
        self.plan = plan
        self.current_step = 0

    def get_next_step(self):
        if self.current_step < len(self.plan):
            return self.plan[self.current_step]
        return None

    def step_completed(self):
        self.current_step += 1

    def is_plan_complete(self):
        return self.current_step >= len(self.plan)

    def checkpoint(self):
        """
        Provides a checkpoint for user interaction.
        Returns the user's choice.
        """
        next_step = self.get_next_step()
        if not next_step:
            print("Plan is complete.")
            return "abort"

        while True:
            prompt = f"""
Next step: {next_step}

Options:
- continue (c): Execute the next step
- skip (s): Skip this step
- edit (e): Edit this step
- abort (a): Abort the plan

Your choice: """
            choice = input(prompt).lower().strip()
            if choice in ['continue', 'c']:
                return 'continue'
            elif choice in ['skip', 's']:
                self.step_completed()
                return 'skip'
            elif choice in ['edit', 'e']:
                new_step = input("Enter the new step: ")
                self.plan[self.current_step] = new_step
                print("Step updated.")
                # Loop again to show the updated step
            elif choice in ['abort', 'a']:
                print("Aborting plan.")
                return 'abort'
            else:
                print("Invalid choice. Please try again.")

    def execute_plan(self):
        """
        Executes the plan with checkpoints.
        This is a simulation and will just print the steps.
        """
        print("Starting plan execution...")
        while not self.is_plan_complete():
            user_choice = self.checkpoint()

            if user_choice == 'continue':
                step = self.get_next_step()
                print(f"Executing: {step}")
                # In a real scenario, you would execute the step here.
                self.step_completed()
            elif user_choice == 'skip':
                print("Step skipped.")
            elif user_choice == 'abort':
                break

        if self.is_plan_complete():
            print("Plan executed successfully.")