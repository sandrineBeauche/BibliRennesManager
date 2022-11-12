import { Component } from '@angular/core';
import {ThemePalette} from '@angular/material/core';
import { HttpClient } from "@angular/common/http";
import { Loan, LoanData } from './Loan';
import { Card, CardData } from './Card';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  title = 'Bibli Rennes Manager GUI';

  background: ThemePalette = undefined;

  items: Loan[] = [];

  cards: Card[] = [];

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
