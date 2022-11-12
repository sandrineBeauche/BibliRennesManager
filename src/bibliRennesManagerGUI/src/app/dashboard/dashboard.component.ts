import { Component, Input, OnInit } from '@angular/core';
import { Card } from '../Card';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  @Input() cards: Card[] = []

  constructor() { }

  ngOnInit() {
  }

}
