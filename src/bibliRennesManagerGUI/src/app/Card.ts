import { Loan } from "./Loan";

export interface CardData{
    name: string;
    cardId: string;
    password: string;
}

export enum CardStatus{
    Ok,
    Late,
    Blocked
}

export enum LibraryNetwork{
    BibliRennes = "Bibliothèques de Rennes",
    ChampsLibres = "Les Champs Libres"
}

export class LibraryStat{
    library: LibraryNetwork;
    nbLoans: number = 0;

    constructor(lib: LibraryNetwork){
        this.library = lib
    }
}

export class Card {
    data: CardData
    loans: LibraryStat[] = [
        new LibraryStat(LibraryNetwork.BibliRennes),
        new LibraryStat(LibraryNetwork.ChampsLibres)
    ]
    back!: LibraryStat | null;
    status: CardStatus = 0;

    constructor(data: CardData){
        this.data = data;
    }
}
