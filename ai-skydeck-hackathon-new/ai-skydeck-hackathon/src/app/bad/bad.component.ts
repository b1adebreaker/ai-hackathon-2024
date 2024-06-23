import { Component } from '@angular/core';
import { BadEmissionsGraphComponent } from '../bad-emissions-graph/bad-emissions-graph.component';
import { CompanyData } from '../interfaces/interfaces.component';
import { CommonModule } from '@angular/common';
import { GetDataService } from '../services/get-data.service';

const MOCK_COMPANY_DATA: CompanyData = {
  2005: {
    report: "chevron_NYSE_CVX_2005.pdf",
    video:"https://www.youtube.com/watch?v=elyMmfUFr-g",
    scope_1: 61000000,
    scope_2: 7000000,
    scope_3: 352000000,
    report_sentiment: 52,
    video_sentiment: "eco-sad"
    
  },
  2006: {
    report:  "chevron_NYSE_CVX_2006.pdf",
    video: "https://www.youtube.com/watch?v=elyMmfUFr-g",
    scope_1: 592000000,
    scope_2: 7600000,
    scope_3: 365000000,
    report_sentiment: 68,
    video_sentiment: "greenhushing-defensive"
  },
  2007: {
    report:  "chevron_NYSE_CVX_2007.pdf",
    video: "https://www.youtube.com/watch?v=elyMmfUFr-g",
    scope_1: 597000000,
    scope_2: 7900000,
    scope_3: 358000000,
    report_sentiment: 60,
    video_sentiment: "eco-sad"
  }
}; 

@Component({
  selector: 'app-bad',
  standalone: true,
  imports: [BadEmissionsGraphComponent, 
            CommonModule],
  templateUrl: './bad.component.html',
  styleUrl: './bad.component.css'
})
export class BadComponent {
  badCompanies: string[] = this.GetDataService.getBadCompanies();
  selectedCompany: string | null = null;
  company: CompanyData | null = null;

  
  constructor(private GetDataService: GetDataService) {}

  setCompany(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    this.selectedCompany = selectElement.value;
    console.log(this.selectedCompany);
    this.getCompanyData();

  }

  getCompanyData(): void {
    if (this.selectedCompany) {
    this.company = MOCK_COMPANY_DATA; //replace later 
    console.log(this.company);
    }
  }

}
