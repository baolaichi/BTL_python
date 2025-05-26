from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models.event import Event
from app.views.event_view import EventForm
from app import db
import os
import secrets
from PIL import Image
from datetime import datetime, timedelta

event_bp = Blueprint('event', __name__)

def save_event_image(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['EVENT_UPLOAD_FOLDER'], picture_fn)
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(current_app.config['EVENT_UPLOAD_FOLDER'], exist_ok=True)
    
    # Resize ảnh
    output_size = (1200, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@event_bp.route('/admin/events')
@login_required
def admin_events():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    events = Event.query.order_by(Event.created_at.desc()).all()
    return render_template('admin/events.html', events=events)

@event_bp.route('/admin/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    form = EventForm()
    if form.validate_on_submit():
        image_file = save_event_image(form.image.data) if form.image.data else None
        
        # Tự động set ngày bắt đầu và kết thúc
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=7)
        
        event = Event(
            title=form.title.data,
            description=form.description.data,
            image=image_file,
            start_date=start_date,
            end_date=end_date,
            is_active=form.is_active.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Sự kiện đã được thêm thành công!', 'success')
        return redirect(url_for('event.admin_events'))
    
    return render_template('admin/add_event.html', form=form)

@event_bp.route('/admin/events/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    
    if form.validate_on_submit():
        if form.image.data:
            # Xóa ảnh cũ
            if event.image:
                try:
                    os.remove(os.path.join(current_app.config['EVENT_UPLOAD_FOLDER'], event.image))
                except FileNotFoundError:
                    pass
            
            # Lưu ảnh mới
            image_file = save_event_image(form.image.data)
            event.image = image_file
        
        event.title = form.title.data
        event.description = form.description.data
        event.is_active = form.is_active.data
        
        db.session.commit()
        flash('Sự kiện đã được cập nhật thành công!', 'success')
        return redirect(url_for('event.admin_events'))
    
    return render_template('admin/edit_event.html', form=form, event=event)

@event_bp.route('/admin/events/<int:id>/delete', methods=['POST'])
@login_required
def delete_event(id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('home.index'))
    
    event = Event.query.get_or_404(id)
    
    # Xóa ảnh
    if event.image:
        try:
            os.remove(os.path.join(current_app.config['EVENT_UPLOAD_FOLDER'], event.image))
        except FileNotFoundError:
            pass
    
    db.session.delete(event)
    db.session.commit()
    flash('Sự kiện đã được xóa thành công!', 'success')
    return redirect(url_for('event.admin_events')) 