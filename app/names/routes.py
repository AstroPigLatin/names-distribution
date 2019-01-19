import csv, codecs
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_required
from app import db
from app.models import RefugeeList
from app.names import bp
from app.names.forms import UploadCSVForm

@bp.route('/success')
@login_required
def success():
    return render_template('names/success.html')

@bp.route('/view_list')
@login_required
def view_list():
    names = RefugeeList.query.all()
    return render_template('names/view_list.html', names=names)

@bp.route('/upload_csv', methods=['GET', 'POST'])
@login_required
def upload_csv():
    form = UploadCSVForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'fileName' not in request.files:
            flash('Please select a .csv file in correct format')
            return redirect(request.url)
        csv_file = request.files['fileName']
        if csv_file:
            csv_reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8', errors='ignore'), delimiter=',')
            next(csv_reader, None) # ignore header
            for row in csv_reader:
                refugee = RefugeeList(identity=row[5], origin=row[6], found_dead=row[3], cause_of_dead=row[7], source=row[8])
                db.session.add(refugee)
                db.session.commit()
            return redirect(url_for('names.success'))
    return render_template('names/upload_csv.html',form=form)

@bp.route('/get_name', methods=['GET', 'POST'])
@login_required
def get_name():

    return render_template('names/get_name.html')