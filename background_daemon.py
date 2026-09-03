        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {
                "error": "Endpoint not found",
            }
            self.wfile.write(json.dumps(error_data).encode())

    def log_message(self, format, *args):
        return

def run_task_loop():
    while True:
        try:
            print("--- Starting Automated Revenue Cycle ---")
            os.makedirs("generated_assets", exist_ok=True)
            dual_engine_generator.generate_dynamic_assets()
            publisher.publish_releases()
            print("--- Revenue Cycle Complete ---")
        except Exception as e:
            print(f"Error in revenue cycle: {e}")
        time.sleep(60)

if __name__ == "__main__":
    t = threading.Thread(target=run_task_loop, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"Monetized API server live on port {port}")
    server.serve_forever()
