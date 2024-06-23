import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CompanyList } from '../interfaces/interfaces.component.js';
import { CompanyData } from '../interfaces/interfaces.component.js';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GetDataService {
  private ApiUrl = "url";

  //constructor(private http: HttpClient) { }

  getGoodCompanies(): string[] {
    // return this.http.get(`${this.apiUrl}/companies`);
    //return companylist.goodCompanies;
    return ["clif bar", "patagonia", "apple", "microsoft", "mezzo", "hume"];
  }

  getBadCompanies(): string[] {
    return ["company1", "company2", "company3", "company4", "company5", "company6"];
  }

  getSelectedCompany(company: string): Observable<CompanyData> {
      //return this.http.get<CompanyData>(`${this.apiUrl}/company/${company}`);
    
    const MOCK_COMPANY_DATA: CompanyData = {
        2005: {
          report: "https://www.responsibilityreports.com/HostedData/ResponsibilityReportArchive/c/NYSE_CVX_2005.pdf",
          video:"https://www.youtube.com/watch?v=elyMmfUFr-g"
        },
        2006: {
          report:  "https://www.responsibilityreports.com/HostedData/ResponsibilityReportArchive/c/NYSE_CVX_2006.pdf",
          video: "https://www.youtube.com/watch?v=elyMmfUFr-g"
        }
      };
    return of(MOCK_COMPANY_DATA);
    }
}


