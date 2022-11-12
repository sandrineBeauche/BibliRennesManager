import { Component, Input, OnInit } from '@angular/core';
import { Card } from 'src/app/Card';

@Component({
  selector: 'app-cards',
  templateUrl: './cards.component.html',
  styleUrls: ['./cards.component.css']
})
export class CardsComponent implements OnInit {

  @Input() cards: Card[] | undefined

  nbCardsColumns: number | undefined;


  fontTitle = {
    color: 'rosybrown',
    size: 20,
    opacity: 0.5,
    family: "'Helvetica Neue', 'Arial'",
    weight: 200
} 

  bibRennesTitle = {
    text: 'Biblis de Rennes',
    font: this.fontTitle 
  }

  champsLibresTitle = {
    text: "Les champs libres",
    font: this.fontTitle
  }

  ticksMinor: any = { interval: 1, size: '5%' };
  ticksMajor: any = { interval: 2, size: '9%' };

  labels : any = {distance: '10px', position: 'inside', interval: 2}

  constructor() { }

  ngOnInit() {
    this.nbCardsColumns = (window.innerWidth <= 600) ? 1 : 2;
  }

  onResize(event: Event) {
    if(event != null){
      let width = (event.target as Window).innerWidth;
      this.nbCardsColumns = (width <= 600) ? 1 : 2;
    }
    
  }

}
