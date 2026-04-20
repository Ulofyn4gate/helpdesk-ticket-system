from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB + table
def init_db():
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              issue TEXT,
              priority TEXT,
              status TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

#Homepage

@app.route("/")
def home():
    return '''
    <h1>Helpdesk Ticket System</h1>
    <form method= "POST" action="/submit">
        Name: <input name="name"><br>
        Issue: <input name="issue"><br>
        Priority:
        <select name="priority">
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
        </select><br>
        <button type= "submit">Submit Ticket</button>
    </form>
    <br>
    <a href="/tickets">View Tickets</a>
    '''

#Submit tickets

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    issue = request.form.get("issue")
    priority = request.form.get("priority")

    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("INSERT INTO tickets (name, issue, priority, status) VALUES (?, ?, ?, ?)", (name, issue, priority, "Open")) 
    conn.commit()
    conn.close()

    return redirect("/tickets")
    
#View tickets
@app.route("/tickets")
def view_tickets():
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tickets")
    tickets = c.fetchall()
    conn.close()

    output = "<h2>All Tickets</h2>"

    for t in tickets:
        output += f"""
        <p>
        ID: {t[0]} | {t[1]} - {t[2]} | Priority: {t[3]} | Status: {t[4]}
        <a href='/resolve/{t[0]}'>Resolve</a> |
        <a href='/delete/{t[0]}'>Delete</a>
        </p>
        """
    output += "<br><a href='/'>Back</a>"
    return output

 #Resolve ticket
@app.route("/resolve/<int:id>")
def resolve(id):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("UPDATE tickets SET status = 'Resolved' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/tickets")

#Delete ticket    
@app.route("/delete<int:id>")
def delete(id):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("DELETE FROM tickets WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/tickets")


if __name__ == "__main__":
    app.run(debug=True)