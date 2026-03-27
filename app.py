import customtkinter as ctk
from database import JobDatabase
from scraper import scrape_job_details

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class JobTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Automated Job Application Tracker")
        self.geometry("800x650")

        self.db = JobDatabase()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.title_label = ctk.CTkLabel(
            self, text="Job Application Tracker", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20,10))

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.url_label = ctk.CTkLabel(self.input_frame, text="Job URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Paste job posting URL here...")
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.add_button = ctk.CTkButton(
            self.input_frame, text="Scrape & Add Job", command=self.add_job_action
        )
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        self.log_box = ctk.CTkLabel(
            self,
            text="System Ready",
            fg_color=("gray80", "gray20"),
            corner_radius=8,
            height=35
        )
        self.log_box.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.dashboard_label = ctk.CTkLabel(
            self, text = "Your Applications", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.dashboard_label.grid(row=3, column=0, padx=20, pady=(15,5), sticky="w")

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0,20))
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.refresh_list()

    def add_job_action(self):
        url = self.url_entry.get()

        if not url:
            self.update_log("Error: Please enter a valid URL")
            return

        self.update_log(f"Processing URL: {url}...")
        self.update()

        company, title = scrape_job_details(url)

        try:
            record_id = self.db.add_job(url=url, company=company, job_title=title)
            self.update_log(f"Success! Saved to database (Record ID: {record_id})")

            self.refresh_list()
        except Exception as e:
            self.update_log(f"Database Error: {e}")

        self.url_entry.delete(0, "end")

    def update_log(self, message):
        self.log_box.configure(text=message)

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        jobs = self.db.get_all_jobs()

        if not jobs:
            empty_label = ctk.CTkLabel(self.scroll_frame, text="No jobs found. Start applying!")
            empty_label.grid(row=0, column=0, pady=20)
            return
        
        for index, job in enumerate(jobs):
            job_id, company, title, status, date_added = job

            row_frame = ctk.CTkFrame(self.scroll_frame)
            row_frame.grid(row=index, column=0, sticky="ew", pady=5, padx=5)
            row_frame.grid_columnconfigure(1, weight=1)

            info_text = f"[{date_added[:10]}]    {company} - {title}"
            info_label = ctk.CTkLabel(row_frame, text=info_text, justify="left")
            info_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            status_var = ctk.StringVar(value=status)
            status_menu = ctk.CTkOptionMenu(
                row_frame,
                values=["Applied", "Interviewing", "Rejected", "Offer"],
                variable=status_var,
                command=lambda new_status, j_id=job_id: self.update_job(j_id, new_status),
                width=120
            )
            status_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            delete_btn = ctk.CTkButton(
                row_frame, text="Delete", fg_color="#d9534f", hover_color="#c9302c", width=60,
                command=lambda j_id=job_id: self.delete_job(j_id)
            )
            delete_btn.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    def update_job(self, job_id, new_status):
        self.db.update_status(job_id, new_status)
        self.update_log(f"Updated job {job_id} to {new_status}")

    def delete_job(self, job_id):
        self.db.delete_job(job_id)
        self.update_log(f"Deleted job {job_id}")
        self.refresh_list()

if __name__ == "__main__":
    app = JobTrackerApp()
    app.mainloop()