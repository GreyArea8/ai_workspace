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
