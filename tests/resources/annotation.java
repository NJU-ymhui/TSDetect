@Disabled
public boolean hasSmell(PsiElement element) {
    if (!shouldTestElement(element)) return false;
    if (!(element instanceof PsiMethod)) return false;

    PsiMethod method = (PsiMethod) element;
    PsiAnnotation[] annotations = method.getModifierList().getAnnotations();

    for (PsiAnnotation annotation : annotations) {
        if (annotation.getQualifiedName() != null) {
            if (annotation.getQualifiedName().contains("Ignore") ||
                annotation.getQualifiedName().contains("Disabled")) {
                return true;
            }
        }
    }
    return false;
}