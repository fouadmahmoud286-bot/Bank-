from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from bank_logic import BankAccount

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_mahmoud_banking'

# In-memory database
accounts = {}

# Translations
translations = {
    'en': {
        'title': 'Simple Banking System',
        'bank_name': 'Bank',
        'welcome': 'Welcome to',
        'slogan': 'Values • Security • Trust',
        'create_account': 'Create Account',
        'full_name': 'Full Name',
        'initial_deposit': 'Initial Deposit (EGP)',
        'or': 'OR',
        'login': 'Login',
        'account_number': 'Account Number',
        'access_account': 'Access Account',
        'dashboard': 'Dashboard',
        'logout': 'Logout',
        'current_balance': 'Current Balance',
        'deposit_money': 'Deposit Money',
        'withdraw_money': 'Withdraw Money',
        'deposit': 'Deposit',
        'withdraw': 'Withdraw',
        'amount_placeholder': 'Amount (EGP)',
        'daily_offers': 'Daily Exclusive Offers',
        'home_loan': 'Home Loan',
        'home_loan_desc': 'Get 2% interest rate for the first year!',
        'apply_now': 'Apply Now',
        'car_insurance': 'Car Insurance',
        'car_insurance_desc': '20% off on premium car insurance today.',
        'details': 'Details',
        'gold_card': 'Gold Card',
        'gold_card_desc': 'Zero fees for the first 3 months.',
        'get_card': 'Get Card',
        'success': 'Success!',
        'error': 'Error!',
        'acc_created': 'Account created successfully! Your Account Number is',
        'invalid_bal': 'Invalid balance amount!',
        'enter_valid': 'Please enter a valid name and positive balance.',
        'invalid_acc_fmt': 'Invalid Account Number format!',
        'acc_not_found': 'Account not found!',
        'not_logged_in': 'Not logged in',
        'amount_positive': 'Amount must be positive',
        'invalid_amount': 'Invalid amount',
        'dep_success': 'Deposit successful!',
        'with_success': 'Withdrawal successful!',
        'insufficient': 'Insufficient funds!',
        'welcome_user': 'Welcome,',
        'lang_btn': 'العربية'
    },
    'ar': {
        'title': 'نظام البنك البسيط',
        'bank_name': 'بنك',
        'welcome': 'مرحباً بك في',
        'slogan': 'قيم • أمان • ثقة',
        'create_account': 'إنشاء حساب',
        'full_name': 'الاسم الكامل',
        'initial_deposit': 'الإيداع الأولي (ج.م)',
        'or': 'أو',
        'login': 'تسجيل الدخول',
        'account_number': 'رقم الحساب',
        'access_account': 'دخول الحساب',
        'dashboard': 'لوحة التحكم',
        'logout': 'خروج',
        'current_balance': 'الرصيد الحالي',
        'deposit_money': 'إيداع أموال',
        'withdraw_money': 'سحب أموال',
        'deposit': 'إيداع',
        'withdraw': 'سحب',
        'amount_placeholder': 'المبلغ (ج.م)',
        'daily_offers': 'العروض اليومية الحصرية',
        'home_loan': 'قرض منزلي',
        'home_loan_desc': 'احصل على فائدة 2% للسنة الأولى!',
        'apply_now': 'قدم الآن',
        'car_insurance': 'تأمين سيارات',
        'car_insurance_desc': 'خصم 20% على التأمين المميز اليوم.',
        'details': 'التفاصيل',
        'gold_card': 'البطاقة الذهبية',
        'gold_card_desc': 'بدون رسوم لأول 3 أشهر.',
        'get_card': 'احصل عليها',
        'success': 'نجاح!',
        'error': 'خطأ!',
        'acc_created': 'تم إنشاء الحساب بنجاح! رقم حسابك هو',
        'invalid_bal': 'مبلغ الرصيد غير صحيح!',
        'enter_valid': 'يرجى إدخال اسم صحيح ورصيد موجب.',
        'invalid_acc_fmt': 'صيغة رقم الحساب غير صحيحة!',
        'acc_not_found': 'الحساب غير موجود!',
        'not_logged_in': 'غير مسجل الدخول',
        'amount_positive': 'يجب أن يكون المبلغ موجباً',
        'invalid_amount': 'مبلغ غير صحيح',
        'dep_success': 'تم الإيداع بنجاح!',
        'with_success': 'تم السحب بنجاح!',
        'insufficient': 'رصيد غير كاف!',
        'welcome_user': 'مرحباً،',
        'lang_btn': 'English'
    }
}

@app.before_request
def before_request():
    if 'lang' not in session:
        session['lang'] = 'en'

@app.context_processor
def inject_text():
    lang = session.get('lang', 'en')
    return dict(text=translations[lang], lang=lang)

@app.route('/set_lang/<lang_code>')
def set_lang(lang_code):
    if lang_code in ['en', 'ar']:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    if 'account_number' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    lang = session.get('lang', 'en')
    t = translations[lang]
    
    name = request.form.get('name')
    try:
        initial_balance = float(request.form.get('initial_balance'))
    except ValueError:
        flash(t['invalid_bal'], 'error')
        return redirect(url_for('index'))

    if not name or initial_balance < 0:
        flash(t['enter_valid'], 'error')
        return redirect(url_for('index'))

    new_account = BankAccount(name, initial_balance)
    accounts[new_account.account_number] = new_account
    session['account_number'] = new_account.account_number
    
    flash(f"{t['acc_created']} {new_account.account_number}", 'success')
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def login():
    lang = session.get('lang', 'en')
    t = translations[lang]

    try:
        account_number = int(request.form.get('account_number'))
    except ValueError:
        flash(t['invalid_acc_fmt'], 'error')
        return redirect(url_for('index'))

    if account_number in accounts:
        session['account_number'] = account_number
        return redirect(url_for('dashboard'))
    else:
        flash(t['acc_not_found'], 'error')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'account_number' not in session:
        return redirect(url_for('index'))
    
    acc_num = session['account_number']
    account = accounts.get(acc_num)
    
    if not account:
        session.pop('account_number', None)
        return redirect(url_for('index'))

    return render_template('dashboard.html', account=account)

@app.route('/logout')
def logout():
    session.pop('account_number', None)
    return redirect(url_for('index'))

@app.route('/deposit', methods=['POST'])
def deposit():
    lang = session.get('lang', 'en')
    t = translations[lang]
    
    if 'account_number' not in session:
        return jsonify({'status': 'error', 'message': t['not_logged_in']})

    acc_num = session['account_number']
    account = accounts.get(acc_num)
    
    try:
        amount = float(request.form.get('amount'))
        if amount <= 0:
             return jsonify({'status': 'error', 'message': t['amount_positive']})
    except ValueError:
        return jsonify({'status': 'error', 'message': t['invalid_amount']})

    account.deposit(amount)
    return jsonify({'status': 'success', 'message': t['dep_success'], 'new_balance': account.balance})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    lang = session.get('lang', 'en')
    t = translations[lang]

    if 'account_number' not in session:
        return jsonify({'status': 'error', 'message': t['not_logged_in']})

    acc_num = session['account_number']
    account = accounts.get(acc_num)
    
    try:
        amount = float(request.form.get('amount'))
        if amount <= 0:
             return jsonify({'status': 'error', 'message': t['amount_positive']})
    except ValueError:
        return jsonify({'status': 'error', 'message': t['invalid_amount']})

    if account.withdraw(amount):
        return jsonify({'status': 'success', 'message': t['with_success'], 'new_balance': account.balance})
    else:
        return jsonify({'status': 'error', 'message': t['insufficient']})

if __name__ == '__main__':
    app.run(debug=True)
