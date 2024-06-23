import { Component } from '@angular/core';
import { EmissionsGraphComponent } from '../emissions-graph/emissions-graph.component';
import { GetDataService } from '../services/get-data.service';
import { CommonModule} from '@angular/common';
import { CompanyData } from '../interfaces/interfaces.component';

const MOCK_COMPANY_DATA: CompanyData = {
  2018: {
    report: "chevron_NYSE_CVX_2005.pdf",
    video:"https://www.youtube.com/watch?v=elyMmfUFr-g",
    scope_1: 61000000,
    scope_2: 23523,
    scope_3: 352000000,
    report_sentiment: 60,
    video_sentiment: "idealistic"
    
  },
  2019: {
    report:  "chevron_NYSE_CVX_2006.pdf",
    video: "https://www.youtube.com/watch?v=elyMmfUFr-g",
    scope_1: 592000000,
    scope_2: 2342,
    scope_3: 365000000,
    report_sentiment: 60,
    video_sentiment: "critical"
  },
  2020: {
    report:  "chevron_NYSE_CVX_2007.pdf",
    video: "https://www.youtube.com/watch?v=elyMmfUFr-g",
    scope_1: 597000000,
    scope_2: 79020000,
    scope_3: 358000000,
    report_sentiment: 70,
    video_sentiment: "genuinely-sustainable"
  }
}; 

@Component({
  selector: 'app-good',
  standalone: true,
  imports: [EmissionsGraphComponent, 
            CommonModule],
  templateUrl: './good.component.html',
  styleUrl: './good.component.css'
})
export class GoodComponent {
  goodCompanies: string[] = this.GetDataService.getGoodCompanies();
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
    this.company = MOCK_COMPANY_DATA;
    console.log(this.company);
    }
  }
}

