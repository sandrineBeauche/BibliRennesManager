import { Component, AfterViewInit, OnChanges, ViewChild, Input, SimpleChanges } from '@angular/core';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { Loan } from 'src/app/Loan';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { LoanStatus } from 'src/app/Loan';


@Component({
  selector: 'app-loans-list',
  templateUrl: './loans-list.component.html',
  styleUrls: ['./loans-list.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '250px'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ]
})
export class LoansListComponent implements AfterViewInit, OnChanges {

  @Input()
  items: Loan[] = [];

  dataSource = new MatTableDataSource<Loan>();

  displayedColumns: string[] = ['cover', 'title', 'library', 'card', 'deadline', 'renewed', 'reserved', 'status', 'expand'];

  expandedElement: Loan| null | undefined

  constructor() { }

  ngOnChanges(changes: SimpleChanges): void {
    this.dataSource.data = this.items;
    this.dataSource.sort = this.sort;
  }

  @ViewChild('empTbSort') sort = new MatSort();

  ngAfterViewInit() {
    this.dataSource.data = this.items;
    this.dataSource.sort = this.sort;
  }


  toggleLoanDetail(element: Loan, event: any){
    this.expandedElement = this.expandedElement === element ? null : element; 
    event.stopPropagation()
  }
}
