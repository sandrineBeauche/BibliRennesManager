import { Component, Input, OnInit } from '@angular/core';
import { Loan } from 'src/app/Loan';

@Component({
  selector: 'app-loan-details',
  templateUrl: './loan-details.component.html',
  styleUrls: ['./loan-details.component.css']
})
export class LoanDetailsComponent implements OnInit {

  @Input() loan!: Loan;

  constructor() { }

  ngOnInit() {
  }

}
