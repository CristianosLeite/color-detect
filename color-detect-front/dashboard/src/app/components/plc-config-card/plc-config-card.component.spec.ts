import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlcConfigCardComponent } from './plc-config-card.component';

describe('PlcConfigCardComponent', () => {
  let component: PlcConfigCardComponent;
  let fixture: ComponentFixture<PlcConfigCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlcConfigCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PlcConfigCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
