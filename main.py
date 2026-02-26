    random.shuffle(options)

    # عرض أزرار الخيارات
    col1, col2 = st.columns(2)
    for i, option in enumerate(options):
        with col1 if i % 2 == 0 else col2:
            if st.button(option, key=option, use_container_width=True):
                if option == correct_ans:
                    st.success("أحسنت! إجابة صحيحة 🎉")
                    st.session_state.score += 1
                else:
                    st.error(f"للأسف خطأ! الصحيح هو: {correct_ans}")
                
                st.session_state.count += 1
                # اختيار كلمة جديدة للسؤال القادم
                st.session_state.current_word = df.sample(1).iloc[0]
                st.rerun()

    st.divider()
    st.info(f"📊 نتيجتك الحالية: {st.session_state.score} من أصل {st.session_state.count}")

except Exception as e:
    st.warning("انتظر! تأكد من رفع ملف الكلمات باسم 'vocab.csv' في نفس الصفحة.")

