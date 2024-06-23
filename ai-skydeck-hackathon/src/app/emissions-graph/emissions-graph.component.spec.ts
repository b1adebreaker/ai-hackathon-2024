import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmissionsGraphComponent } from './emissions-graph.component';

describe('EmissionsGraphComponent', () => {
  let component: EmissionsGraphComponent;
  let fixture: ComponentFixture<EmissionsGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmissionsGraphComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EmissionsGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
