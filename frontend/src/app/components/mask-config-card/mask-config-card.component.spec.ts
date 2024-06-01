import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MaskConfigCardComponent } from './mask-config-card.component';

describe('MaskConfigCardComponent', () => {
  let component: MaskConfigCardComponent;
  let fixture: ComponentFixture<MaskConfigCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MaskConfigCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MaskConfigCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
