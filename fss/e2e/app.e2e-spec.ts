import { FssPage } from './app.po';

describe('fss App', () => {
  let page: FssPage;

  beforeEach(() => {
    page = new FssPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
