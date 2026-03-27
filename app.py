import customtkinter as ctk
from database import JobDatabase

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class JobTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Automated Job Application Tracker")
        self.geometry("600x400")

        self.db = JobDatabase()

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self, text="Job Application Tracker", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20,10))

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.url_label = ctk.CTkLabel(self.input_frame, text="Job URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Paste job posting URL here...")
        self.url_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        self.add_button = ctk.CTkButton(
            self, text="Scrape & Add Job", command=self.add_job_action
        )
        self.add_button.grid(row=2, column=0, padx=20, pady=20)

        self.log_box = ctk.CTkTextbox(self, height=150)
        self.log_box.grid(row=3, column=0, padx=20, pady=(0,20), sticky="nsew")
        self.log_box.insert("0.0", "System Ready\n")
        self.log_box.configure(state="disabled")

    def add_job_action(self):
        url = self.url_entry.get()

        if not url:
            self.update_log("Error: Please enter a valid URL")
            return

        self.update_log(f"Processing URL: {url}...")
        #TODO: Web scrapping logic
        temp_company = "Unknown Company"
        temp_title = "Unknown Role"

        try:
            record_id = self.db.add_job(url=url, company=temp_company, job_title=temp_title)
            self.update_log(f"Success! Saved to database (Record ID: {record_id})")
        except Exception as e:
            self.update_log(f"Database Error: {e}")

        self.url_entry.delete(0, "end")

    def update_log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message+"\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

if __name__ == "__main__":
    app = JobTrackerApp()
    app.mainloop()