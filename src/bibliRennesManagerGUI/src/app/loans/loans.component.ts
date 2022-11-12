import { Component, OnInit } from '@angular/core';
import { Loan, LoanData, LoanStatus } from '../Loan';
import { Card, CardStatus, CardData} from '../Card';
import { HttpClient } from "@angular/common/http";

@Component({
  selector: 'app-loans',
  templateUrl: './loans.component.html',
  styleUrls: ['./loans.component.css']
})
export class LoansComponent implements OnInit {

  items: Loan[] = []

  cards: Card[] = []

  constructor(private httpClient: HttpClient) { }

  ngOnInit(): void {
    //Called after the constructor, initializing input properties, and the first call to ngOnChanges.
    //Add 'implements OnInit' to the class.
    this.httpClient.get("assets/items.json").subscribe(dataLoans =>{
      this.httpClient.get("assets/cards.json").subscribe(dataCards => {
        const indexedCards = Object.assign({}, ...(dataCards as CardData[]).map((x) => ({[x.cardId]: new Card(x)})));
        const loans = (dataLoans as LoanData[]).map(val => new Loan(val, indexedCards[val.cardId]));
        this.items = loans;
        const c = Object.values(indexedCards) as Card[];
        this.cards = c;
      })
    });
  }
  
}
