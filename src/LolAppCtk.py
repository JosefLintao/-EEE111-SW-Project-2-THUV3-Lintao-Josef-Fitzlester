from LolDb import LolDb
from LolGuiCtk import LolGuiCtk

def main():
    db = LolDb(init=False, dbName='LolDb.csv')
    app = LolGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()