import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { GoodComponent } from './good/good.component';
import { BadComponent } from './bad/bad.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, 
            GoodComponent, 
            BadComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'my-angular-project';
}
