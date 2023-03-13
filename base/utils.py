from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def create_invoice_pdf(invoice):
    template = get_template('invoice.html')
    context = {'invoice': invoice}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF creation error')
    return response.content
