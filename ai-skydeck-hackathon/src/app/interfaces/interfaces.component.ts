import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface CompanyList {
  good_companies: string[];
  bad_companies: string[];
}

export interface CompanyData {
[year: number]: {
  report: string;
  video: string;
}
}

@Component({
  selector: 'app-interfaces',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './interfaces.component.html',
  styleUrl: './interfaces.component.css'
})

export class InterfacesComponent {

}
