import { Pipe, PipeTransform } from '@angular/core';
import { LoanStatus } from './Loan';

@Pipe({
  name: 'status'
})
export class StatusPipe implements PipeTransform {

  transform(value: LoanStatus, args?: any): any {
    switch (value) {
      case LoanStatus.Ok:
        return "assets/ok_status.png"
      case LoanStatus.Soon:
        return "assets/soon_status.png"
      case LoanStatus.Late:
        return "assets/late_status.png"
      case LoanStatus.Blocking:
        return "assets/blocked_status.png"
      default:
        return "assets/ok_status.png"
    }
  }

}
