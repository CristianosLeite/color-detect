import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ControllerConfigCardComponent } from './controller-config-card.component';

describe('ControllerConfigCardComponent', () => {
  let component: ControllerConfigCardComponent;
  let fixture: ComponentFixture<ControllerConfigCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ControllerConfigCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ControllerConfigCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
