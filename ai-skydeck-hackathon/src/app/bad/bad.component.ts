import { Component } from '@angular/core';
import { BadEmissionsGraphComponent } from '../bad-emissions-graph/bad-emissions-graph.component';

@Component({
  selector: 'app-bad',
  standalone: true,
  imports: [BadEmissionsGraphComponent],
  templateUrl: './bad.component.html',
  styleUrl: './bad.component.css'
})
export class BadComponent {

}
