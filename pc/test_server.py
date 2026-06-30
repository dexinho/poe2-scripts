from flask import Flask
from threading import Thread

# from auto_buy import auto_buy
from test import test

app = Flask(__name__)

# Shared state between threads
state = {"max_items_reached": False}


@app.route("/poe2/scripts/auto_buy/status")
def status():
    return {"max_items_reached": state["max_items_reached"]}


def run_test():
    result = test()
    state["max_items_reached"] = result


def run_server():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    Thread(target=run_test, daemon=True).start()

    run_server()
