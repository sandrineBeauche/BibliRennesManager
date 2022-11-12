import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';

import { MaterialModule } from './material.module';

import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoansComponent } from './loans/loans.component';
import { LoansListComponent } from './loans/loans-list/loans-list.component';
import { CartsComponent } from './loans/carts/carts.component';
import { LoanDetailsComponent } from './loans/loans-list/loan-details/loan-details.component';
import { CardsComponent } from './dashboard/cards/cards.component';

import { LibraryPipe } from './library.pipe';
import { StatusPipe } from './status.pipe';
import { GravatarModule } from 'ngx-gravatar';
import { jqxGaugeModule }  from 'jqwidgets-ng/jqxgauge'; 


@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    LoansComponent,
    LoansListComponent,
    LoanDetailsComponent,
    CartsComponent,
    CardsComponent,
    LibraryPipe,
    StatusPipe
  ],
  imports: [
    BrowserAnimationsModule, 
    BrowserModule,
    AppRoutingModule, 
    MaterialModule,
    HttpClientModule,
    GravatarModule,
    jqxGaugeModule
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
