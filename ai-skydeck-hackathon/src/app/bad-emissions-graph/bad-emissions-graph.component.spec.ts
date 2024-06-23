import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BadEmissionsGraphComponent } from './bad-emissions-graph.component';

describe('BadEmissionsGraphComponent', () => {
  let component: BadEmissionsGraphComponent;
  let fixture: ComponentFixture<BadEmissionsGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BadEmissionsGraphComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(BadEmissionsGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
