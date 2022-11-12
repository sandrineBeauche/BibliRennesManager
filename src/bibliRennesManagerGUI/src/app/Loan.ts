import { Card, CardStatus } from "./Card";

export interface Examplar {
    localisation: string,
    cote: string,
    status: string,
    condition: string
}

export interface Book {
    title: string,
    authors: string,
    url: string,
    notes: string,
    description: string,
    publication: string,
    resume: string,
    cover: string,
    exemplaires: Array<Examplar>
}

export interface LoanData{
    book: Book;
    barcode: string;
    cote: string;
    library: string;
    deadline: Date;
    reservation: boolean;
    renewed: boolean;
    status: string;
    cardId: string;
}

export enum LoanStatus{
    Ok,
    Soon,
    Late,
    Blocking
}

export class Loan {
    book: Book;
    barcode: string;
    cote: string;
    library: string;
    deadline: Date;
    reservation: boolean;
    renewed: boolean;
    status: string;
    cardName: string;

    card: Card | null;
    back: boolean = false;
    itemStatus: LoanStatus | null = 0;

    constructor(data: LoanData, card: Card){
      this.book = data.book;
      this.barcode = data.barcode;
      this.cote = data.cote;
      this.library = data.library;
      this.deadline = data.deadline;
      this.reservation = data.reservation;
      this.renewed = data.renewed;
      this.status = data.status;
      this.cardName = card.data.name;

      this.analyzeStatus()
      this.card = card;
      
      if(this.library.includes("Champs Libres")){
        card.loans[1].nbLoans++;
      }
      else{
        card.loans[0].nbLoans++;
        if(this.itemStatus == LoanStatus.Blocking){
          card.status = CardStatus.Blocked;
        }
      }
      if(this.itemStatus == LoanStatus.Late && card.status == CardStatus.Ok){
        card.status = CardStatus.Late
      }
    }

    analyzeStatus(){
      const delta = new Date(this.deadline).getTime() - Date.now();
      const nbDays = Math.round(delta / (1000 * 3600 * 24))
      if(nbDays > 5){
        this.itemStatus = LoanStatus.Ok;
        return;
      }
      if(nbDays > 0){
        this.itemStatus = LoanStatus.Soon;
        return;
      }
      if(nbDays > -7){
        this.itemStatus = LoanStatus.Late;
        return;
      }
      else{
        this.itemStatus = LoanStatus.Blocking;
        return;
      }
    }

    isSoon(){
      return this.itemStatus == LoanStatus.Soon
    }

    isLate(){
      return this.itemStatus == LoanStatus.Late
    }

    isBlocking(){
      return this.itemStatus == LoanStatus.Blocking
    }
}
