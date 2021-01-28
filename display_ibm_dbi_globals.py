""" Display Database API Global Information"""
import ibm_db_dbi

meaning_threadsafety = {
    0: "Threads may not share the module.",
    1: "Threads may share the module, but not connections.",
    2: "Threads may share the module and connections.",
    3: "Threads may share the module, connections and cursors."
}

meaning_paramstyle = {
"qmark":	r"Question mark style, e.g. ...WHERE name=?",
"numeric":	r"Numeric, positional style, e.g. ...WHERE name=:1",
"named":	r"Named style, e.g. ...WHERE name=:name",
"format":	r"ANSI C printf format codes, e.g. ...WHERE name=%s",
"pyformat":	r"Python extended format codes, e.g. ...WHERE name=%(name)s"
}

print(ibm_db_dbi.apilevel)      # expectiong "2.0"
print(ibm_db_dbi.threadsafety,  meaning_threadsafety[ibm_db_dbi.threadsafety])
print(ibm_db_dbi.paramstyle,    meaning_paramstyle[ibm_db_dbi.paramstyle])

