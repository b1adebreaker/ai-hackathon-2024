import { Component } from '@angular/core';
import { EmissionsGraphComponent } from '../emissions-graph/emissions-graph.component';
import { GetDataService } from '../services/get-data.service';
import { CommonModule} from '@angular/common';
import { CompanyData } from '../interfaces/interfaces.component';

const MOCK_COMPANY_DATA: CompanyData = {
  2005: {
    report: "chevron_NYSE_CVX_2005.pdf",
    video:"https://www.youtube.com/watch?v=elyMmfUFr-g"
  },
  2006: {
    report:  "chevron_NYSE_CVX_2006.pdf",
    video: "https://www.youtube.com/watch?v=elyMmfUFr-g"
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

