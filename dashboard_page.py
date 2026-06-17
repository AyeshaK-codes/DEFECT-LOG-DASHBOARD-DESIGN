from database_manager import get_dashboard_metrics  # Pull database live numbers!
import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("light")

class ColgateDashboard(ctk.CTk):
    def __init__(self, current_user="Guest User"):
        super().__init__()
        
        # Pull live operational data rows out of the sqlite schema map
        self.db_metrics = get_dashboard_metrics()
        
        self.title("Outcrowd SAP Portal")
        self.geometry("1250x820")
        self.configure(fg_color="#f3f4f6")  
        
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=5)  
        self.grid_rowconfigure(2, weight=4)  
        
        self.grid_columnconfigure(0, weight=6) 
        self.grid_columnconfigure(1, weight=4) 
        
        # Setup application components
        self.create_header_row(current_user)
        self.create_top_section()
        self.create_bottom_section()

    def create_header_row(self, user):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=25, pady=(20, 5))
        
        title_label = ctk.CTkLabel(
            header_frame, text="Outcrowd Analytics", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold"), text_color="#111827"
        )
        title_label.pack(side="left")
        
        status_container = ctk.CTkFrame(header_frame, fg_color="#ffffff", corner_radius=20, height=32, border_width=1, border_color="#e5e7eb")
        status_container.pack(side="right")
        status_container.pack_propagate(False)
        
        display_name = user.split('@')[0] if "@" in str(user) else str(user)
        status_label = ctk.CTkLabel(
            status_container, text=f"● Available for work  |  User: {display_name} ",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#10b981"
        )
        status_label.pack(padx=15, pady=2)

    def create_top_section(self):
        # CARD 1: Payments Funnel (Top Left)
        card_payments = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=16)
        card_payments.grid(row=1, column=0, padx=(25, 12), pady=12, sticky="nsew")
        
        # Row Configurations to keep layout stable and anchored when window scales
        card_payments.grid_rowconfigure(0, weight=0) # Title
        card_payments.grid_rowconfigure(1, weight=1) # Chart space (takes expanding height)
        card_payments.grid_rowconfigure(2, weight=0) # AI container fixed at bottom
        card_payments.grid_columnconfigure(0, weight=1)
        
        # FIXED: Changed anchor="w" to sticky="w" for proper grid compliance
        lbl_pay = ctk.CTkLabel(card_payments, text="Payments", font=ctk.CTkFont(family="Inter", size=16, weight="bold"), text_color="#111827")
        lbl_pay.grid(row=0, column=0, sticky="w", padx=24, pady=(20, 10))
        
        chart_mock = ctk.CTkFrame(card_payments, fg_color="#f9fafb", corner_radius=12, border_width=1, border_color="#f3f4f6")
        chart_mock.grid(row=1, column=0, sticky="nsew", padx=24, pady=10)
        
        chart_lbl = ctk.CTkLabel(chart_mock, text="[ Custom Bar Chart Display ]\nInitiated (65.2k) ➔ Authorized (54.8k) ➔ Successful (48.6k)", font=ctk.CTkFont(size=12), text_color="#9ca3af")
        chart_lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # Responsive Intelligent Search / Query Bar Element
        ai_container = ctk.CTkFrame(card_payments, fg_color="#eff6ff", corner_radius=10, border_width=1, border_color="#dbeafe")
        ai_container.grid(row=2, column=0, sticky="ew", padx=24, pady=(10, 20))
        
        ai_title = ctk.CTkLabel(ai_container, text="✦ What would you like to explore next?", font=ctk.CTkFont(family="Inter", size=11, weight="bold"), text_color="#2563eb")
        ai_title.pack(anchor="w", padx=16, pady=(8, 2))
        
        self.ai_input = ctk.CTkEntry(
            ai_container, placeholder_text="Type a question (e.g. drop-off, volume, customers) and press Enter...",
            fg_color="#ffffff", border_width=1, border_color="#e5e7eb", height=36, font=ctk.CTkFont(family="Inter", size=12)
        )
        self.ai_input.pack(fill="x", padx=16, pady=(2, 12))
        self.ai_input.bind("<Return>", self.process_ai_query)

        # CARD 2: Gross Volume (Top Right)
        card_gross = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=16)
        card_gross.grid(row=1, column=1, padx=(12, 25), pady=12, sticky="nsew")
        
        lbl_gross = ctk.CTkLabel(card_gross, text="Gross Volume", font=ctk.CTkFont(family="Inter", size=14, weight="bold"), text_color="#6b7280")
        lbl_gross.pack(anchor="w", padx=24, pady=(20, 2))
        
        gross_value_string = self.db_metrics.get("gross_volume", ("$0", 1.0))[0]
        val_gross = ctk.CTkLabel(card_gross, text=gross_value_string, font=ctk.CTkFont(family="Inter", size=38, weight="bold"), text_color="#111827")
        val_gross.pack(anchor="w", padx=24, pady=(0, 15))
        
        breakdown_box = ctk.CTkFrame(card_gross, fg_color="transparent")
        breakdown_box.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        
        segments = [
            ("Online Payments", "online_payments", "#10b981"), 
            ("Subscriptions", "subscriptions", "#3b82f6"), 
            ("In-Store Sales", "instore_sales", "#ec4899")
        ]
        for title, db_key, color in segments:
            amt, pct = self.db_metrics.get(db_key, ("$0", 0.0))
            
            row = ctk.CTkFrame(breakdown_box, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=title, font=ctk.CTkFont(family="Inter", size=12), text_color="#4b5563").pack(side="left")
            ctk.CTkLabel(row, text=amt, font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#111827").pack(side="right")
            
            pbar = ctk.CTkProgressBar(breakdown_box, progress_color=color, fg_color="#f3f4f6", height=6)
            pbar.set(pct)
            pbar.pack(fill="x", pady=(2, 8))

    def create_bottom_section(self):
        card_retention = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=16)
        card_retention.grid(row=2, column=0, padx=(25, 12), pady=(12, 25), sticky="nsew")
        
        lbl_ret = ctk.CTkLabel(card_retention, text="Retention", font=ctk.CTkFont(family="Inter", size=16, weight="bold"), text_color="#111827")
        lbl_ret.pack(anchor="w", padx=24, pady=(20, 10))
        
        ret_graph_mock = ctk.CTkFrame(card_retention, fg_color="#ffffff")
        ret_graph_mock.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        
        canvas_line = tk.Canvas(ret_graph_mock, bg="#ffffff", highlightthickness=0)
        canvas_line.pack(fill="both", expand=True)
        canvas_line.create_line(10, 120, 80, 80, 140, 95, 210, 40, 280, 110, 350, 100, 450, 130, fill="#ec4899", width=3)

        bottom_right_grid = ctk.CTkFrame(self, fg_color="transparent")
        bottom_right_grid.grid(row=2, column=1, padx=(12, 25), pady=(12, 25), sticky="nsew")
        bottom_right_grid.grid_columnconfigure(0, weight=1)
        bottom_right_grid.grid_columnconfigure(1, weight=1)
        bottom_right_grid.grid_rowconfigure(0, weight=1)
        bottom_right_grid.grid_rowconfigure(1, weight=1)
        
        tx_val = self.db_metrics.get("transactions", ("0", 1.0))[0]
        card_tx = ctk.CTkFrame(bottom_right_grid, fg_color="#ffffff", corner_radius=16)
        card_tx.grid(row=0, column=0, padx=(0, 6), pady=(0, 6), sticky="nsew")
        ctk.CTkLabel(card_tx, text="Transactions", font=ctk.CTkFont(family="Inter", size=13, weight="bold"), text_color="#4b5563").pack(anchor="w", padx=16, pady=(15, 2))
        ctk.CTkLabel(card_tx, text=tx_val, font=ctk.CTkFont(family="Inter", size=26, weight="bold"), text_color="#111827").pack(anchor="w", padx=16)
        
        cust_val = self.db_metrics.get("customers", ("0", 1.0))[0]
        card_cust = ctk.CTkFrame(bottom_right_grid, fg_color="#ffffff", corner_radius=16)
        card_cust.grid(row=1, column=0, padx=(0, 6), pady=(6, 0), sticky="nsew")
        ctk.CTkLabel(card_cust, text="Customers", font=ctk.CTkFont(family="Inter", size=13, weight="bold"), text_color="#4b5563").pack(anchor="w", padx=16, pady=(15, 2))
        ctk.CTkLabel(card_cust, text=cust_val, font=ctk.CTkFont(family="Inter", size=26, weight="bold"), text_color="#111827").pack(anchor="w", padx=16)

        card_insights = ctk.CTkFrame(bottom_right_grid, fg_color="#1e1b4b", corner_radius=16) 
        card_insights.grid(row=0, column=1, rowspan=2, padx=(6, 0), pady=0, sticky="nsew")
        
        ins_pill = ctk.CTkFrame(card_insights, fg_color="#2e2a75", corner_radius=12, height=24, width=70)
        ins_pill.pack(anchor="w", padx=20, pady=(20, 10))
        ins_pill.pack_propagate(False)
        ctk.CTkLabel(ins_pill, text="Insights", font=ctk.CTkFont(family="Inter", size=11), text_color="#ffffff").pack()
        
        ctk.CTkLabel(card_insights, text="75%", font=ctk.CTkFont(family="Inter", size=48, weight="bold"), text_color="#ffffff").pack(anchor="w", padx=20)
        
        self.ai_insights_label = ctk.CTkLabel(
            card_insights, text="Authorization rate increased by 4% compared to last week.\n\nType a question in the AI bar above and press Enter to update this panel live!",
            font=ctk.CTkFont(family="Inter", size=12), text_color="#94a3b8", justify="left", wraplength=140
        )
        self.ai_insights_label.pack(anchor="w", padx=20, pady=10)

    def process_ai_query(self, event=None):
        """Parses the natural language query string and maps context back to the insights target."""
        query_text = self.ai_input.get().strip().lower()
        
        if not query_text:
            return
            
        response = "I recognized your query, but I need specific tracking terms like 'drop-off', 'volume', or 'customers' to extract relevant data points."
        
        # Match Scenario 1: Funnel metrics / conversion barriers
        if "drop" in query_text or "fail" in query_text or "authorized" in query_text:
            response = "AI Analysis: The 11.3% drop-off from authorized (54.8k) to successful (48.6k) payments is driven by legacy card timeouts. Switching routing to path B can rescue ~$6,200."
            
        # Match Scenario 2: High-level financial lookups
        elif "volume" in query_text or "sales" in query_text or "revenue" in query_text:
            gross_amt = self.db_metrics.get("gross_volume", ("$41,540", 1.0))[0]
            response = f"AI Analysis: Current Gross Volume is resting at {gross_amt}. Online channels represent your highest performing vector, with subscriptions expanding by 2.4%."
            
        # Match Scenario 3: Human Capital metrics / User directories
        elif "customer" in query_text or "user" in query_text:
            cust_count = self.db_metrics.get("customers", ("1,284", 1.0))[0]
            response = f"AI Analysis: Active transacting reach stands at {cust_count} profiles. Growth metrics remain steady, keeping churn below 3.1% this reporting period."

        # Housekeeping: Clear entry layout and push the new string onto the UI panel frame
        self.ai_input.delete(0, tk.END)
        self.ai_insights_label.configure(text=response, text_color="#e0e7ff")


if __name__ == "__main__":
    app = ColgateDashboard()
    app.mainloop()