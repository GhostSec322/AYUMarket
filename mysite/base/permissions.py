from rest_framework import permissions

# 리뷰 기능에서 쓰는 권한 설정
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 비로그인도 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 본인이 작성한 것에만 허용
        return obj.user == request.user