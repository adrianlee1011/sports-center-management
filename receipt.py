from fpdf import FPDF

class PDF(FPDF):

    def header(self):
        # add company logo to receipt
        self.image('/Users/callumdavey-turner/PycharmProjects/untitled1/sports_centre.png', 10, 8, 33)

        # receipt title
        self.set_font("Arial", 'B', 13)
        self.cell(80)
        self.cell(30, 10, 'Your Reciept!',1,0, 'C')
        self.ln(5)
        # sports centre address
        self.set_font("Arial", '', 8)
        self.cell(180, 8, 'The Sports Centre', 0,0, 'R')
        self.ln(5)
        self.cell(180, 8, 'University of Leeds', 0,0, 'R')
        self.ln(5)
        self.cell(180, 8, 'LS2, 9JT', 0, 0, 'R')

        self.ln(20)


    def footer(self):
        # footer with aut page numbering
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def create_PDF(customer_name, order_number, email_address):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'I', 8)


   # main body of receipt

    pdf.cell(0, 10, 'Order number:              ' + order_number, 0, 1)
    pdf.dashed_line(10,45,200,45,1,1)

    pdf.cell(0,10, 'Customer Name:              ' + customer_name, 0, 1)
    pdf.dashed_line(10,55,200,55,1,1)

    pdf.cell(0,10, 'Email Address:              ' + email_address, 0, 1)
    pdf.dashed_line(10, 65, 200, 65, 1, 1)


    pdf.cell(0, 10, 'DATE', 1, 0,'C')
    pdf.cell(0, 10, 'TIME', 1, 0,'C')
    pdf.cell(0, 10, 'FACILITY', 1, 0,'C')
    pdf.cell(0, 10, 'PRICE', 1, 1,'C')

    pdf.cell(0, 10, 'TIME', 1, 0, 'C')
    pdf.cell(0, 10, 'FACILITY', 1, 0, 'C')
    pdf.cell(0, 10, 'PRICE', 1, 1, 'C')




    # manipulate this so the path isn't local
    pdf_path = '/Users/callumdavey-turner/PycharmProjects/untitled1/'+ order_number + '.pdf'

    # outputs to given path
    pdf.output(pdf_path, 'F')


create_PDF('Callum', 'order4562', 'callumdt48@gmail.com')
create_PDF('Adrian', 'order466', 'Adrian@gmail.com')