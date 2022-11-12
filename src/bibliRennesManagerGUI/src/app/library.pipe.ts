import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'library'
})
export class LibraryPipe implements PipeTransform {

  transform(value: string, args?: any): any {
    if(value.includes("Les Champs Libres")){
      return "assets/champsLibres.png"
    }
    else{
      return "assets/bibliRennes.jpeg"
    }
  }

}
