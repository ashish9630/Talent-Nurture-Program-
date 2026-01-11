import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Flats } from './flats';

describe('Flats', () => {
  let component: Flats;
  let fixture: ComponentFixture<Flats>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Flats]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Flats);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
